class Rental:
  """
  A class to store housing info
  """
  def __init__(self, name: str, cost: int, beds: int, distance: int, location: str, link: str):
    self.name = name
    self.cost = cost
    self.beds = beds
    self.distance = distance
    self.location = location
    self.link = link
  
  def __str__(self):
    return f"""{self.name}\nCost: {self.cost} with {self.beds} beds\nIt is {self.distance}km from UVic in {self.location} \n{self.link}"""

  def get_name(self):
    return self.name
  
  def set_name(self,name:str):
    self.name = name

  def get_cost(self):
    return self.cost

  def set_cost(self,cost:int):
    self.cost = "${:,.2f}".format(cost)

  def get_beds(self):
    return self.beds

  def set_beds(self,beds:int):
    self.beds = beds

  def get_location(self):
    return self.location

  def set_loc(self,location:str):
    self.location = location

  def get_distance(self):
    return self.distance

  def set_distance(self,distance:int):
    self.distance = distance

  def get_link(self):
    return self.link
  
  def set_link(self,link:str):
    self.link = link

#  def get_keys(self):
#    return ["name","cost","beds","loc","dist","link"]