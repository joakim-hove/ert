#  Copyright (C) 2011  Statoil ASA, Norway. 
#   
#  The file 'stat.py' is part of ERT - Ensemble based Reservoir Tool. 
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details. 


import ctypes
import libutil
import tvector 
from   ert.cwrap.cwrap       import *

def quantile( data , q ):
    return cfunc.quantile( data , q )


def quantile_sorted( data , q ):
    return cfunc.quantile_sorted( data , q )


cwrapper = CWrapper( libutil.lib )
cfunc    = CWrapperNameSpace("stat")


cfunc.quantile        = cwrapper.prototype("double statistics_empirical_quantile( double_vector , double )")
cfunc.quantile_sorted = cwrapper.prototype("double statistics_empirical_quantile( double_vector , double )")
