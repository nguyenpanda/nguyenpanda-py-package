import cProfile

from _utility_performance import print_profile
from nguyenpanda.nguyenpanda.butterfly import RandomORG


def randint():
    generator.randint(1, 1, 6)


def randint_seq():
    generator.randint_seq(5, 5, 1, 10)


def usage():
    generator.usage()


def uuid4():
    generator.uuid4(5)


def blobs():
    generator.blobs(5, 16)


def strings():
    generator.strings(10, 10, "hatuongnguyen")


def decimal():
    generator.decimal(5, 14)


def gauss():
    generator.gauss(5, 0, 1, 14)


if __name__ == "__main__":
    API = 'ENTER_YOUR_API'

    with cProfile.Profile() as profile:
        generator = RandomORG(API)
        randint()
        randint_seq()
        usage()
        uuid4()
        blobs()
        strings()
        decimal()
        gauss()

    print_profile(profile, __file__)
