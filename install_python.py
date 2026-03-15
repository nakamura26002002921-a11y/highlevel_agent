# highlevel_agent/install_python.py
from lowlevel_agent.install_python.agent import installpython

def run():
    installpython("3.11.6", "/opt/python3.11")
    

if __name__ == "__main__":
    run()