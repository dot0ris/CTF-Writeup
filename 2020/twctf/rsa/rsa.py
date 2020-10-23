import angr

proj = angr.Project('./rsa', load_options={'auto_load_libs': False})
path_group = proj.factory.path_group(threads=4)
path_group.explore(find=0xFB7, avoid=0xFC5)
print(path_group.found[0].state.posix.dumps(1))