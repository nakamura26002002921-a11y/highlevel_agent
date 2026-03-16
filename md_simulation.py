import lowlevel_agent.md_simulation.agent as agent
PATH = ""
PDB_PATH = None
WATER_MODEL = None
FORCE_FIELD = None
WATERBOXFILE = None
DISTANCE = None
GMX = "gmx"

def start():
    agent.initialization(PATH)
    return "getpdbfile"

def get_pdb():
    result = agent.get_pdb(PATH, "1ALC")
    if not result:
        return "error"
    PDB_PATH = result
    return "simulation_set"

def simulation_set():
    result = agent.simulation_set(PATH)
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
        GMX = GMX
    ) else "error"

def minimization():
    return "nvt" if agent.minimization(PATH) else "error"

def nvt():
    return "npt_br" if agent.nvt(PATH) else "error"

def npt_br():
    return "npt_pr" if agent.npt_br(PATH) else "error"

def npt_pr():
    return "finish" if agent.npt_pr(PATH) else "error"

def error():
    print("simulation failed")
    return "finish"

FUNCTIONS = {
    "start": start,
    "getpdbfile": get_pdb,
    "simulation_set": simulation_set,
    "system_build": system_build,
    "minimization": minimization,
    "nvt": nvt,
    "npt_br": npt_br,
    "npt_pr": npt_pr,
    "error": error,
}
def run():
    state = "start"
    while state != "finish":
        print("state:", state)
        try:
            state = FUNCTIONS[state]()
        except KeyError:
            print("unknown state:", state)
            break
    print("finished")
if __name__ == "__main__":
    run()
