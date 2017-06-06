def B(M):
    q_M = '''print "''' + M + '''"\n'''
    print M + q_M
    
def A(): 
    return r"""def B(M):
    q_M = '''print "''' + M + '''"\n'''
    return M + q_M\n"""
