from copy import deepcopy
class Paper(object):
    def __init__(self, bf , gsm , deck ,color):
        self.bf = bf
        self.gsm = gsm
        self.deck = deck
        self.color = color

class Roll(object):
    def __init__(self, name, weight, paper):
        self.name = name
        self.weight = weight
        self.paper = paper
    def roll_show(self):
      print "Roll Name: %s" % self.name
      print " Weight : %s " % ( self.weight )
      print "Color: " + self.paper.color

class UsedRolls(object):
    def __init__(self, roll_name, starting_weight, finished_weight):
        self.roll_name = roll_name
        self.starting_weight = starting_weight
        self.finished_weight = finished_weight

class Box(object):
    def __init__(self , name , length , width , height , ply ):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.ply = ply


class BoxDescription(object):
    def __init__(self, box, paper, top_paper, box_per_board ):
        self.box = box
        self.box_per_board = box_per_board
        self.board_len = 2 * ( box.length + box.width )
        self.board_deck = box.width + box.height
        self.layers = {"top": top_paper, "flute": paper, "liner" : paper}
        self.per_board_liner_weight = self.get_liner_layer_weight()
        self.per_board_top_weight = self.get_top_layer_weight()

    def box_desc_show(self):
        print "Box Name: " + self.box.name
        print "Box Details: Length: %s, Width: %s, Height: %s, Ply: %s" % (self.box.length , self.box.width , self.box.height , self.box.ply )
        print " Board Length: %s, Board Width: %s" % (self.board_len , self.board_deck)
        print "Paper used for Flute: %s" % self.layers["flute"].color + "\nPaper used for Liner : %s" % self.layers["liner"].color + "\nPaper used for Top: %s" % self.layers["top"].color

    def get_liner_layer_weight(self):
        return float((self.board_len * self.board_deck * self.layers["liner"].gsm)) / (10000000) # Calculate Per board Liner Weigh

    def get_top_layer_weight(self):
        return float((self.board_len * self.board_deck * self.layers["top"].gsm)) / (10000000)

    def rolls_selection(self, available_rolls, used_rolls_list, layer, quantity):
        if layer == "flute":
            layer_weight = float(1.5 * (quantity / self.box_per_board) * self.per_board_liner_weight) # Total Flute Weight
            print "Total flute Weight: " + str(layer_weight) + "Kg"
        elif layer == "liner":
            layer_weight = (quantity / self.box_per_board) * float(self.per_board_liner_weight) # Total Liner Weight
            print "\nTotal liner Weight: " + str(layer_weight) + "Kg"
        elif layer == "top":
            layer_weight = (quantity / self.box_per_board) * float(self.per_board_top_weight)
            print "\nTotal top Weight: " + str(layer_weight) + "Kg"
        count = 0
        roll_sum = 0
        i = 0
        for roll in available_rolls:
            if self.layers[layer].color == roll.paper.color and self.layers[layer].gsm == roll.paper.gsm and self.layers[layer].deck == roll.paper.deck:
                roll_sum += roll.weight
                print "Roll sum: " +str(roll_sum) + "\nPresent Roll display: " + str(roll.weight)
                if roll_sum <= layer_weight:
                    used_roll = UsedRolls(roll.name, roll.weight, 0)
                    print str(used_roll.roll_name) + "\n" + str(used_roll.starting_weight)
                    used_rolls_list.append(used_roll)
                    roll.weight=0
                    print str(roll.weight) + "\n" + str(used_roll.starting_weight)
                else:
                    original_weight = roll.weight
                    remaining_weight = roll_sum - layer_weight
                    roll.weight = original_weight - remaining_weight
                    used_roll = UsedRolls(roll.name, original_weight, roll.weight)
                    used_rolls_list.append(used_roll)
                    roll.weight = remaining_weight
            if (roll_sum >= layer_weight): break
            i += 1
        return i

    def get_box_count(self, rolls):
        print "\nPer_board_liner_weight(in kg): " + str(self.per_board_liner_weight) + "\nper_board_top_weight(in kg): " + str(self.per_board_top_weight)
        board_weight = float(self.per_board_liner_weight) + (1.5 * self.per_board_liner_weight) + self.per_board_top_weight
        box_weight = float(board_weight) / self.box_per_board # Single Box Weight
        print "Board Weight(in kg): " + str(board_weight) + "\nBox Weight(in kg): " + str(box_weight)
        used_rolls_list = []
        i = self.rolls_selection(rolls, used_rolls_list, "flute", 10000)
        j = i
        temp_weight = rolls[i].weight
        rolls[i].weight = 0
        i = self.rolls_selection(rolls, used_rolls_list, "liner", 10000)
        rolls[j].weight = temp_weight
        rolls.sort(key = lambda Rolls: Rolls.weight)
        i = self.rolls_selection(rolls, used_rolls_list, "top", 10000)
        sum = 0
        print "Used Rolls: ",
        for i in used_rolls_list:
            if i.finished_weight == 0:
                sum += i.starting_weight
            else:
                sum += i.finished_weight
            print "[" + str(i.roll_name) + ", " + str(i.starting_weight) +", "+ str(i.finished_weight) + "]",
        box_count = ( sum / box_weight )
        print "\nAvailable Rolls: ",
        for i in rolls:
            print "[" + str(i.name) + ", " + str(i.weight) + "]",
        print "\n Used Rolls Sum: %s" % sum + "Kg"
        print " Box Count: %s " % int(box_count)


paper = Paper(16, 180, 96, "Brown")
paper_180_96 = Paper(16, 230, 96, "White")

rolls = [Roll(42650, 500, paper), Roll(42651, 350, paper), Roll(42652, 450, paper_180_96), Roll(42653, 370, paper), Roll(42654, 470, paper_180_96), Roll(42655, 480, paper)]
rolls.sort(key=lambda Roll:Roll.weight, reverse=True)
print "Available Rolls(in Kg): %s, %s, %s, %s, %s, %s" % (rolls[0].weight,rolls[1].weight, rolls[2].weight, rolls[3].weight, rolls[4].weight, rolls[5].weight)
box1 = Box("Bhakthi" , 42 , 22 , 25, 3)
box2 = Box("Ganesh" , 45 , 24 , 26 , 5)

box1_desc = BoxDescription(box1 ,paper, paper_180_96, 2)
#box2_desc = BoxDescription(box2 ,paper, paper, 1)

box1_desc.box_desc_show()
#box2_desc.box_desc_show()

box1_desc.get_box_count(rolls)
#box1_desc.get_box_count(rolls)
#box2_desc.get_box_count(rolls)
#box2_desc.get_box_count(rolls)
