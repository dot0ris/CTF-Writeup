'''
import angr

proj = angr.Project('../googlectf/beginner/a.out', load_options={'auto_load_libs': False})
path_group = proj.factory.path_group(threads=4)
path_group.explore(find=0x111D, avoid=0x1100)
print(path_group.found[0].state.posix.dumps(1))
'''
import angr #the main framework
import claripy #the solver engine

proj = angr.Project("./power", auto_load_libs=False)
sym_arg_size = 16 #Length in Bytes because we will multiply with 8 later
sym_arg = claripy.BVS('sym_arg', 8*sym_arg_size)
state = proj.factory.full_init_state(args=["./power"], stdin=sym_arg)
for byte in sym_arg.chop(8):
    state.add_constraints(byte >= '\x20') # ' '
    state.add_constraints(byte <= '\x7e') # '~'
simgr = proj.factory.simulation_manager(state)
avoid_addr = 0x10003898
find_addr = 0x10003888
simgr.explore(find=find_addr, avoid=avoid_addr)
found = simgr.found[0]
print(found.posix.dumps(0))