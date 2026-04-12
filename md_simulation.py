import lowlevel_agent.md_simulation.agent as agent
PATH = "your_path_here"
PDBID = ""
REFERENCE_MDP_PATH = None
simulation_info = ""
GMX = "gmx"
PYMOL = "pymol"
PDB_PATH = None
WATER_MODEL = None
FORCE_FIELD = None
WATERBOXFILE = None
DISTANCE = None

def start():
    agent.initialization(PATH)
    return "get_pdb"

def get_pdb():
    global PDB_PATH
    result = agent.get_pdb(PATH, PDBID)
    if not result:
        return "error"
    PDB_PATH = result
    return "copy_mdp"

def copy_mdp():
    return "simulation_set" if agent.copy_mdp(PATH, REFERENCE_MDP_PATH) else "error"

def simulation_set():
    global WATER_MODEL, FORCE_FIELD, WATERBOXFILE, DISTANCE
    result = agent.simulation_set(PATH, simulation_info)
    if not result:
        return "error"
    WATER_MODEL, FORCE_FIELD, WATERBOXFILE, DISTANCE = result
    return "system_build"

def system_build():
    return "minimization" if agent.system_build(
        PATH,
        pdb_path=PDB_PATH,
        FF=FORCE_FIELD,
        DISTANCE=DISTANCE,
        WATER_MODEL=WATER_MODEL,
        WATERBOXFILE=WATERBOXFILE,
        GMX=GMX,
        PYMOL=PYMOL,
    ) else "error"

def minimization():
    return "nvt" if agent.minimization(PATH, GMX=GMX) else "error"

def nvt():
    return "npt_br" if agent.nvt(PATH, GMX=GMX) else "error"

def npt_br():
    return "npt_pr" if agent.npt_br(PATH, GMX=GMX) else "error"

def npt_pr():
    return "md" if agent.npt_pr(PATH, GMX=GMX) else "error"

def md():
    return "finish" if agent.md(PATH, GMX=GMX) else "error"

def error():
    print("❌ simulation failed")
    return "finish"

def run():
    state = "start"
    while state != "finish":
        print(f"▶ state: {state}")
        func = globals().get(state)
        if not func:
            print(f"❌ unknown state: {state}")
            break
        try:
            state = func()
        except Exception as e:
            print(f"💥 error in {state}: {e}")
            state = "error"
    print("✅ finished")

if __name__ == "__main__":
    run()
