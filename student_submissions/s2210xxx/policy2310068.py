from policy import Policy
import numpy as np

class Policy2310068(Policy):
  def __init__(self):
    # Student code here
    self.stock_info_list = []
    self.stock_idx = []
    self.stock_sheets = []
    self.sorted_list_prods = []
    self.first_action = False
  
  def SortProducts(self, products):
    return sorted(products, key=lambda x:-x["size"][0]*x["size"][1])

  def SortStockSheet(self, stocks):
    self.stock_info_list = []
    self.stock_idx = []
    self.stock_sheets = []
    for i, stock in enumerate(stocks):
      w, h = self._get_stock_size_(stock)
      self.stock_info_list.append((w*h, i, stock))
    self.stock_info_list = sorted(self.stock_info_list, key=lambda x: x[0], reverse=True)
    self.stock_idx = [item[1] for item in self.stock_info_list]
    self.stock_sheets = [item[2] for item in self.stock_info_list]


  def CanCut(self, stockSheet, pos, prod):
    return self._can_place_(stockSheet, pos, prod["size"])
  
  def CutProduct(self, product, stockSheet):
    stock_width, stock_height = self._get_stock_size_(stockSheet)
    product_width, product_height = product["size"]
    # if product is not cuttable in this current stock, move to the next stock
    if (product_width < 0 or product_width > stock_width or product_height < 0 or product_height > stock_height):
      pass
    else:
      #Initialize the first cutting posititon, (-1, -1) means the product hasn't been cut
      cut_position = (-1, -1)
      # Iterate through every possible place that can cut the product
      for x in range(0, stock_width - product_width + 1):
        for y in range(0, stock_height - product_height + 1):
          # If can cut the product, save the cut posittion
          if (stockSheet[x][y] != -1):
            continue
          else:
            if (self.CanCut(stockSheet, (x, y), product)):
              cut_position = (x, y)
              break
        # If finded cuttable posittion, out the loop
        if (cut_position[0] != -1 and cut_position[1] != -1):
          break
    return cut_position


  def get_action(self, observation, info):
    # Student code here
    if (self.first_action == False or info["filled_ratio"] == 0.00):
      self.first_action = True
      # Sort stock sheets based on area in decending order 
      self.SortStockSheet(observation["stocks"])
      # Sort products based on area in decending order    
      self.sorted_list_prods = self.SortProducts(observation["products"])

    for i in range (0, len(self.stock_sheets)):
      for product in self.sorted_list_prods:
        if product["quantity"] > 0:
          product_size = product["size"]
          cut_position = self.CutProduct(product, self.stock_sheets[i])
          if cut_position[0] != -1 and cut_position[1] != -1:
            stock_idx = self.stock_idx[i]
            break
          else:
            continue
      if cut_position[0] != -1 and cut_position[1] != -1:
        break
      else:
        continue
    return {"stock_idx": stock_idx, "size": product_size, "position": cut_position}

    # # Loop thourgh products list and try to cut the largest product for each stock
    # for product in self.sorted_list_prods:
    #   # Only accept product which has quantity greater than 0
    #   if product["quantity"] > 0:
    #     product_size = product["size"]
    #      # Loop through every stock, trying to fit the largest product as possible
    #     for i in range(0, len(self.stock_sheets)):
    #       cut_position = self.CutProduct(product, self.stock_sheets[i])
    #       if (cut_position[0] != -1 and cut_position[1] != -1):
    #         stock_idx = self.stock_idx[i]
    #         break
    #     if (cut_position[0] != -1 and cut_position[1] != -1):
    #       break
    # return {"stock_idx": stock_idx, "size": product_size, "position": cut_position}

    # Student code here
    # You can add more functions if needed
