import os
import pstats
import cProfile

from nguyenpanda.nguyenpanda.swan import Color


def print_profile(profile: cProfile.Profile, output_file: str) -> None:
    output_file = str(os.path.basename(output_file).removesuffix('.py')) + '.prof'

    result = pstats.Stats(profile)
    result.sort_stats(pstats.SortKey.TIME)
    result.print_stats()

    result.dump_stats(output_file)

    # noinspection PyUnresolvedReferences
    print('in %.3f seconds' % result.total_tt, file=result.stream)

    Color.print('If you want to interact with data on web browser run:', color='g')
    print('  >> ', end='')
    Color.print(f'tuna {output_file}', color='c')
