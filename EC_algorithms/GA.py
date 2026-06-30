import EC_algorithms.MA as MA


def Search(robot_m, options, prefix, evaluator, local_search, logger, pbar):
  options.local_search_algorithm = None
  return MA.Search(robot_m, options, prefix, evaluator, local_search, logger, pbar)
