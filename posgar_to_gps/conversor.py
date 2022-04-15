from math import atan, exp, floor, pi, cos, sin, sqrt, tan
from typing import Dict, NamedTuple

from posgar_to_gps import SUCCESS


class ConversionResponse(NamedTuple):
    lat_long: Dict[str, float]
    error: int

class Conversor:
  def __init__(self, x: str, y:str, zone:str) -> None:
      self._x = x
      self._y = y
      self._zone = zone
  
  def convert(self, as_degrees: bool):
    [lat, long] = calcuXY(self._x, self._y, self._zone)
    if as_degrees:
      return ConversionResponse({"lat": agrad(lat), "long": agrad(long)}, SUCCESS)
    else:
      return ConversionResponse({"lat": lat, "long": long}, SUCCESS)

def calcuXY(X,Y,zone):
  f=1
  FE=1000000*zone+500000
  FN=10001965.729
  loncero=(3*zone-75)*pi/180
  Y=Y-FN;X=X-FE
  epri=0.0820944380368543
  c=6399593.62580398
  fipri=Y/(6366197.724*f)
  sigma=c*f/sqrt(1+pow((epri*cos(fipri)),2))
  a=X/sigma
  A1=sin(2*fipri)
  A2=A1*pow(cos(fipri),2)
  J2=fipri+A1/2
  J4=(3*J2+A2)/4
  J6=(5*J4+A2*pow(cos(fipri),2))/3
  alzone=(3/4)*pow(epri,2)
  beta=(5/3)*pow(alzone,2)
  gama=(35/27)*pow(alzone,3)
  Bfi=f*c*(fipri-alzone*J2+beta*J4-gama*J6)
  b=(Y-Bfi)/sigma
  zeta=(1/2)*pow((epri*a*cos(epri)),2)
  epsi=a*(1-zeta/3)
  eta=fipri+b*(1-zeta)
  lon=atan(((exp(epsi)-exp((-1*epsi)))/2)/cos(eta))
  tau=atan((cos(lon))*(tan(eta)))
  lon=lon+loncero
  lat=fipri+(1+pow((epri*cos(fipri)),2)-(3/2)*pow(epri,2)*(sin(fipri))*(cos(fipri))*(tau-fipri))*(tau-fipri)
  lon=lon*180/pi;lat=lat*180/pi
  lat=round(lat*100000000)/100000000;lon=round(lon*100000000)/100000000;
  coor= [lat, lon]
  return coor

def agrad(argu):
  sig=abs(argu)/argu
  argu=abs(argu)
  grad=floor(argu)
  min=(argu-grad)*60
  seg=(min-floor(min))*60
  min=floor(min)
  if((round(seg*1000))/1000==60):
    seg=0
    min=min+1
  gms="{}º {}' {}\"".format(sig*grad, min, (round(seg*1000))/1000)
  return gms