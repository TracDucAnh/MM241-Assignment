from policy import Policy
import math

class Policy2310068(Policy):
    def __init__(self, policy_id=1):
        assert policy_id in [1, 2], "Policy ID must be 1 or 2"

        self.policy_id = policy_id
        # Student code here
        if policy_id == 1:
          self.policy_name = "FFD_modified"
          self.stock_info_list = []
          self.stock_idx = []
          self.stock_sheets = []
          self.sorted_list_prods = []
          self.first_action = False

        elif policy_id == 2:
            self.policy_name = "CCF_heuristic"
            self.sequencePosReturn = []
            self.products = []
            self.stock_sheets = [] # Priority cutting large stocks
            self.stock_idx = [] # Keep track of stock index after sort stocksheets
            self.sorted_list_prods = [] # Priority process large products
            self.curr_stock = []
            self.component_stack_for_curr_stock = [] # Store a stack of components each time we cut
            self.undominated_products = [] # Store list of undominate product 
            self.sequence_actions_for_curr_stock = [] # If sequence actions for 1 stock is empty, move to another stock otherwise continue return action
            self.first_action = False


    ###################################################### Define methods for both policy ######################################################
    # Function to sort products
    def SortProducts(self, products):
      return sorted(products, key=lambda x:-x["size"][0]*x["size"][1])
    
    # Function to sort stocksheets
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
    
    #Function to determine if we could cut the product on a position on a stocksheet
    def CanCut(self, stockSheet, pos, prod_size):
      return self._can_place_(stockSheet, pos, prod_size)
    
    ###################################################### End define methods for both policy ######################################################   

    ###################################################### Define methods for FFD modified ######################################################    
    #Function to cut, rotate
    def CutProduct(self, product_size, stockSheet):
      stock_width, stock_height = self._get_stock_size_(stockSheet)
      product_width, product_height = product_size
      # if product is not cuttable in this current stock, move to the next stock
      if (product_width < 0 or product_width > stock_width or product_height < 0 or product_height > stock_height):
        pass
      else:
        product_size = product_size
        #Initialize the first cutting posititon, (-1, -1) means the product hasn't been cut
        cut_position = (-1, -1)
        # Iterate through every possible place that can cut the product
        for x in range(0, stock_width - product_width + 1):
          for y in range(0, stock_height - product_height + 1):
            # If can cut the product, save the cut posittion
            if (stockSheet[x][y] != -1):
              continue
            else:
              if (self.CanCut(stockSheet, (x, y), product_size)):
                cut_position = (x, y)
                product_size = product_size
                break
          # If finded cuttable posittion, out the loop
          if (cut_position[0] != -1 and cut_position[1] != -1):
            break
      return cut_position, product_size

    # Action for FFD
    def get_action_FFD_modified(self, observation, info):
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
            cut_position, product_size = self.CutProduct(product["size"], self.stock_sheets[i])
            # Rotate to find if rotated product could fit the remain area
            if (cut_position[0] == -1 or cut_position[1] == -1):
              cut_position, product_size = self.CutProduct(product["size"][::-1], self.stock_sheets[i])
            
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
    ###################################################### End define methods for FFD modified ######################################################


    ###################################################### Define methods for CCF algorithm ######################################################
    def update_products(self, observation):
        self.products = []
        NewDictProducts = observation["products"]
        SortedListProds = self.SortProducts(NewDictProducts)
        # products list after sorted and eliminate product with quantity == 0
        for product in SortedListProds:
            if (product["quantity"] == 0):
                continue
            else:
              self.products.append(product)

    def GetUndominateProducts(self):
        numProd = len(self.products)
        self.undominateProds = []
        for i in range (0, numProd):
            dominatedFlag = False
            current_prod_width, current_prod_height = self.products[i]["size"]
            for j in range(0, numProd):
                  other_width, other_height = self.products[j]["size"]
                  if (current_prod_height < other_height and current_prod_width < other_width):
                      dominatedFlag = True
            if (dominatedFlag == True):
                continue
            else:
                self.undominateProds.append(self.products[i])  

    def CCF(self, observation, currStockSheet):
       pass

    def get_action_CCF(self, observation, info):
        pass
    ###################################################### End define mothods for CCF algorithm ######################################################


    def get_action(self, observation, info):
        # Student code here
        if self.policy_id == 1:
          return self.get_action_FFD_modified(observation, info)
        elif self.policy_id == 2:
          return self.get_action_CCF(observation, info)
    # Student code here
    # You can add more functions if needed