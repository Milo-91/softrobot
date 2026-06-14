import robot.basicrobot as robot_m
import itertools

r1 = robot_m.get_random()
print(r1.id)
print(r1.shape)
r2 = robot_m.get_random()
print(r2.id)
print(r2.shape)
r3 = r2.copy()
print(r3.id)
print(r3.shape)

r4 = robot_m.mutate(r1)
print(r4.id)
print(r4.shape)

r5 = robot_m.crossover(r2, r4)
print(r5.id)
print(r5.shape)

r5.set_score(60)
print(r5.score)


r5_shape = list(itertools.chain(*r5.shape.tolist()))
r2_shape = list(itertools.chain(*r2.shape.tolist()))
print(r5_shape)
print(r2_shape)
print(sum(r5 != r2 for r5, r2 in zip(r5_shape, r2_shape)))

