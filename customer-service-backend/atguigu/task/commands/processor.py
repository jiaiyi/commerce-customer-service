from typing import List

from atguigu.domain.contexts import TaskContext, StartedSystemContext, InterruptedSystemContext, CanceledSystemContext, \
    ResumedSystemContext
from atguigu.domain.state import DialogueState
from atguigu.task.commands.models import Command, StartFlowCommand, SetSlotsCommand, CancelFlowCommand, \
    ResumeFlowCommand
from atguigu.task.flows.models import FlowsList, Flow


class CommandProcessor:
    def process_command(self,commands:List[Command],state:DialogueState,flows_list:FlowsList) -> None :
        for command in commands:
            if isinstance(command,StartFlowCommand):
                self._handle_start_flow(command,state,flows_list)
            elif isinstance(command,SetSlotsCommand):
                self._handle_set_slots(command,state)
            elif isinstance(command,CancelFlowCommand):
                self._handle_cancel_flow(state,flows_list)
            elif isinstance(command,ResumeFlowCommand):
                self._handle_resume_flow(command,state,flows_list)

    def _handle_start_flow(self, command:StartFlowCommand, state:DialogueState,flows_list:FlowsList):
        """
            StartFlowCommand(command="start_flow",flow="refund_request")
        """
        # 1.获取目标flow：从StartFlowCommand获取flow_id，再根据flow_id从flows_list中获取flow
        flow_id = command.flow
        target_flow:Flow = flows_list.get_flow_by_id(flow_id)
        if target_flow:
            # 2.获取用户任务上下文
            current_task = state.active_task
            # 3.判断是否有正在执行的用户任务
            if current_task:
                # 有正在执行的任务
                state.interrupt_active_task()
                # 启动目标任务（创建一个用户任务上下文）
                state.start_task(TaskContext(
                    flow_id=flow_id,
                    step_id=target_flow.get_start_step().id
                ))
                # 启动system_task-interrupted系统任务（创建系统任务上下文）
                state.start_system_task(InterruptedSystemContext(
                    flow_id="system_task_interrupted",
                    step_id=flows_list.get_flow_by_id("system_task_interrupted").get_start_step().id,
                    interrupted_flow_id=current_task.flow_id,
                    interrupted_flow_name=flows_list.get_flow_by_id(current_task.flow_id).name,
                    started_flow_id=flow_id,
                    started_flow_name=target_flow.name
                ))
            else:
                # 没有正在执行的任务，
                # 启动目标任务（创建一个用户任务上下文）
                state.start_task(TaskContext(
                    flow_id=flow_id,
                    step_id=target_flow.get_start_step().id
                ))
                # 启动system_task_started系统任务（创建系统任务上下文）
                state.start_system_task(StartedSystemContext(
                    flow_id="system_task_started",
                    step_id=flows_list.get_flow_by_id("system_task_started").get_start_step().id,
                    started_flow_id=flow_id,
                    started_flow_name=target_flow.name
                ))
    def _handle_set_slots(self,command:SetSlotsCommand,state:DialogueState):
        """
        : SetSlotsCommand(command="set_slots", slots={"order_number":"A20260001"})
        """
        # 1.从SetSlotsCommand中获取slots
        slots = command.slots
        # 2.（只要生成了set_slots指令，就一定会有一个正在执行的任务）
        if state.active_task:
            state.set_slots(slots)

    def _handle_cancel_flow(self, state:DialogueState, flows_list:FlowsList):
        # 1.从state中获取当前正在运行的用户任务上下文
        current_task = state.active_task
        if current_task:
            # 2.取消当前任务
            state.cancel_active_task()
            # 3.启动sys_task_canceled系统任务
            state.start_system_task(CanceledSystemContext(
                flow_id="system_task_canceled",
                step_id=flows_list.get_flow_by_id("system_task_canceled").get_start_step().id,
                canceled_flow_id=current_task.flow_id,
                canceled_flow_name=flows_list.get_flow_by_id(current_task.flow_id).name
            ))
            
    def _handle_resume_flow(self,command:ResumeFlowCommand,state:DialogueState,flows_list:FlowsList):
        """
        ResumeFlowCommand(command="resume_flow", flow="refund_request")
        """
        # 1.获取目标flow
        target_flow_id = command.flow
        target_flow = flows_list.get_flow_by_id(target_flow_id)
        # 2.获取用户任务上下文
        current_task = state.active_task
        # 3.判断是否有正在执行的用户任务
        if current_task:
            state.interrupt_active_task()
            #恢复目标任务
            state.resume_task(target_flow_id)
            # 启动system_task_resumed系统任务
            state.start_system_task(InterruptedSystemContext(
                flow_id="system_task_resumed",
                step_id=flows_list.get_flow_by_id("system_task_resumed").get_start_step().id,
                interrupted_flow_id=current_task.flow_id,
                interrupted_flow_name=flows_list.get_flow_by_id(current_task.flow_id).name,
                started_flow_id=target_flow_id,
                started_flow_name=target_flow.name
            ))
        else:
            state.resume_task(target_flow_id)
            # 启动system_task_interrupt系统任务
            state.start_system_task(ResumedSystemContext(
                flow_id="system_task_resumed",
                step_id=flows_list.get_flow_by_id("system_task_resumed").get_start_step().id,
                resumed_flow_id=target_flow_id,
                resumed_flow_name=target_flow.name
            ))



