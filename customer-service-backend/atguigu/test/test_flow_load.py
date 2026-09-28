from pathlib import Path

from atguigu.task.flows.loader import FlowLoader

if __name__ == '__main__':
    user_flows_path = Path(__file__).parents[2]/'flow_config'/'user_flows.yml'
    system_flows_path = Path(__file__).parents[2]/'flow_config'/'system_flows.yml'
    loader = FlowLoader()
    flows_list = loader.load_many( [user_flows_path, system_flows_path] )
    print( flows_list )