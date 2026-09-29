from typing import Dict, Any

from jinja2 import Template
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.infrastructure.ai_clients import llm_client
from atguigu.prompts.history_builder import build_history
from atguigu.task.action.base import Action, ActionResult


class ActionResponse(Action):

    name = "action_response"

    async def run(self,state:DialogueState,args:Dict[str,Any]) -> ActionResult:
        mode = args.get("mode","static")
        if mode == "static":
            # 静态模式创建机器回复
            text = args.get("text","")
            data = {
                "slots": state.active_task.slots if state.active_task else {},
                "context": state.active_system_task.to_dict() if state.active_system_task else {},
            }
            rendered_text = Template(text).render(data)
            return ActionResult(
                messages=[BotMessage(text=rendered_text)],
            )
        elif mode == "rephrase":
            # 改写模式创建机器回复
            # 1.获取text并渲染
            text = args.get("text","")
            data = {
                "slots": state.active_task.slots if state.active_task else {},
                "context": state.active_system_task.to_dict() if state.active_system_task else {},
            }
            rendered_text = Template(text).render(data)
            # 2.调用llm对渲染后的回复消息进行改写
            prompt_text = args.get("prompt","""你是一个中文电商客服助手，语气自然、友好、简洁。
                                                请结合对话上下文，把下面的建议回复改写得更自然，但不要改变含义。
                                            
                                                对话历史：
                                                {{ history }}
                                            
                                                用户最后一句：
                                                {{ user_message }}
                                            
                                                建议回复：{{ current_response }}""")
            prompt_inputs = {
                "history": build_history(state.get_current_session().turns),
                "user_message": state.pending_turn.input_message.text,
                "current_response": rendered_text
            }
            prompt = PromptTemplate.from_template(
                prompt_text,
                template_format="jinja2"
            )
            chain = prompt | llm_client | StrOutputParser()
            rephrased_text = chain.invoke(prompt_inputs)
            # 3.讲改写后的内容构造为botmessage返回
            return ActionResult(
                messages=[BotMessage(text=rephrased_text)],
            )
        else:
            # 直接生产机器回复
            prompt_text = args.get("prompt", """你是一个中文电商客服助手，语气自然、友好、简洁。
                                                            请结合对话上下文，把下面的建议回复改写得更自然，但不要改变含义。

                                                            对话历史：
                                                            {{ history }}

                                                            用户最后一句：
                                                            {{ user_message }}

                                                            建议回复：{{ current_response }}""")
            prompt_inputs = {
                "history": build_history(state.get_current_session().turns),
                "user_message": state.pending_turn.input_message.text
            }
            prompt = PromptTemplate.from_template(
                prompt_text,
                template_format="jinja2"
            )
            chain = prompt | llm_client | StrOutputParser()
            generated_text = chain.invoke(prompt_inputs)
            return ActionResult(
                messages=[BotMessage(text=generated_text)],
            )