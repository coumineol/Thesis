#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Volkan
#
# Created:     13/04/2014
# Copyright:   (c) Volkan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re

def parser(list):
    newlist = []
    for variant in list:
        newvariant = []
        for score in variant:
            x = float((re.findall(r'\(.*\)', score))[0][1:-1])
            newvariant.append(x)
        newlist.append(newvariant)
    return newlist

if __name__ == '__main__':
    main()
