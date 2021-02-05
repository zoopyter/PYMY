#EGConvention
#egpricing_python_project
#---------------------------------------------------------
from enum import Enum
#---------------------------------------------------------

class EGConvention():
#---------------------------------------------------------
# Business Convention
#---------------------------------------------------------
    class BusConv:
        class Basis(str, Enum):
            Following = "F"
            ModifiedFollowing = "MF"
            Preceding = "P"
            ModifiedPreceding = "MP"
            Unadjusted = "U"
            Nearest = "NE"

#---------------------------------------------------------
# Date Generator
#---------------------------------------------------------
    class DateGen(str, Enum):
        Forward = "F"
        Backward = "B"
        Zero = "Z"
        ThirdWednesDay = "TD"
        Twentieth = "TW"
        TwentiethIMM = "I"
        CDS = "C"


