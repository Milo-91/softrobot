def record_md(filename, content=None, robot=None):
    with open(filename, 'a') as f:
        if content != None:
            print(content, file=f)
        if robot != None:
            print(f'## {robot.id}', file=f)
            print(f'score: {robot.score}', file=f)
            print(*(robot.shape.tolist()), sep='\n', file=f)
