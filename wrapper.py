import os

import datawrapper as dw
import repo_mongo as rm


def main():
    dw.load_data_mongo()
    #datawrapper.load_data_cassandra()
    rm.setup()
    rm.get_songs_with_tag()

def parseArgs():
    pass

if __name__ == "__main__":
    main()