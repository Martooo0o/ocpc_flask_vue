from datetime import datetime

class Apriori():

    def __init__(self, dataset):
        self.dataset = dataset
        self.freq_itemsets = []
        self.support_data = {}
        self.confidence_data = {}
        self.t_num = float(len(self.dataset))
        self.assoc_rules = []
        self.num_items = {}


    def __create_C1(self):
        """
        Create frequent candidate 1-itemset C1 by scaning data set.
        Args:
            data_set: A list of transactions. Each transaction contains several items.
        Returns:
            C1: A set which contains all frequent candidate 1-itemsets
        """
        C1 = set()
        print('Datase: ')
        print(self.dataset)
        for t in self.dataset:
            # print(t)
            for item in t:
                # print(item)
                item_set = frozenset([item])
                C1.add(item_set)
        return C1


    def __is_apriori(self, Ck_item, Lksub1):
        """
        Judge whether a frequent candidate k-itemset satisfy Apriori property.
        Args:
            Ck_item: a frequent candidate k-itemset in Ck which contains all frequent
                    candidate k-itemsets.
            Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
        Returns:
            True: satisfying Apriori property.
            False: Not satisfying Apriori property.
        """
        for item in Ck_item:
            sub_Ck = Ck_item - frozenset([item])
            if sub_Ck not in Lksub1:
                return False
        return True


    def __create_Ck(self, Lksub1, k):
        """
        Create Ck, a set which contains all all frequent candidate k-itemsets
        by Lk-1's own connection operation.
        Args:
            Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
            k: the item number of a frequent itemset.
        Return:
            Ck: a set which contains all all frequent candidate k-itemsets.
        """
        Ck = set()
        len_Lksub1 = len(Lksub1)
        list_Lksub1 = list(Lksub1)
        for i in range(len_Lksub1):
            for j in range(1, len_Lksub1):
                l1 = list(list_Lksub1[i])
                l2 = list(list_Lksub1[j])
                l1.sort()
                l2.sort()
                if l1[0:k-2] == l2[0:k-2]:
                    Ck_item = list_Lksub1[i] | list_Lksub1[j]
                    # pruning
                    if self.__is_apriori(Ck_item, Lksub1):
                        # self.assoc_rules.append([(Lksub1, Ck_item), ])
                        Ck.add(Ck_item)
        return Ck


    def __generate_Lk_by_Ck(self, Ck, min_sup, min_conf):
        """
        Generate Lk by executing a delete policy from Ck.
        Args:
            data_set: A list of transactions. Each transaction con tains several items.
            Ck: A set which contains all all frequent candidate k-itemsets.
            min_sup: The minimum support.
            support_data: A dictionary. The key is frequent itemset and the value is support.
        Returns:
            Lk: A set which contains all frequent k-itemsets.
        """
        Lk = set()
        item_count = {}
        for t in self.dataset:
            for item in Ck:
                if item.issubset(t):
                    if item not in item_count:
                        item_count[item] = 1
                    else:
                        item_count[item] += 1

        for item in item_count.keys():
            supp_x_to_y = item_count[item] / self.t_num
            my_count = 0
            if (item_count[item] / self.t_num) >= min_sup:
                Lk.add(item)
                self.support_data[item] = item_count[item] / self.t_num
                for freq_set in self.freq_itemsets:  # at this point freq_itemsets contains only items from k-1 size
                    if set(freq_set[0]).issubset(item):
                        conf_x_to_y = item_count[item] / self.num_items[len(freq_set[0])][freq_set[0]]
                        if conf_x_to_y>min_conf:
                            x = list(freq_set[0])
                            x.sort()
                            y = [x for x in item if x not in freq_set[0]]
                            y.sort()
                            conf = item_count[item] / self.t_num
                            self.assoc_rules.append([ x , y, conf])

        item_from_Ck = None
        for x in Ck:
            item_from_Ck = x
            break
        if(item_from_Ck is not None):
            self.num_items[len(item_from_Ck)] = item_count
        return Lk


    def generate_L(self, min_sup, min_conf):
        """
        Generate all frequent itemsets.
        Args:
            data_set: A list of transactions. Each transaction contains several items.
            k: Maximum number of items for all frequent itemsets.
            min_sup: The minimum support.
        Returns:
            L: The list of Lk.
            support_data: A dictionary. The key is frequent itemset and the value is support.
        """
        start = datetime.now()
        C1 = self.__create_C1()
        deltatime = datetime.now() - start
        create_Ck_time = deltatime.seconds + deltatime.microseconds / 1000000
        
        start = datetime.now()
        L1 = self.__generate_Lk_by_Ck(C1, min_sup, min_conf)
        deltatime = datetime.now() - start
        generate_Lk_time = deltatime.seconds + deltatime.microseconds / 1000000
        
        Lksub1 = L1.copy()
        for lk_i in Lksub1:
            self.freq_itemsets.append((lk_i, self.support_data[lk_i]))
        i = 2

        while True:
            start = datetime.now()
            Ci = self.__create_Ck(Lksub1, i)
            deltatime = datetime.now() - start
            create_Ck_time += deltatime.seconds + deltatime.microseconds / 1000000

            start = datetime.now()
            Li = self.__generate_Lk_by_Ck(Ci, min_sup, min_conf)
            deltatime = datetime.now() - start
            generate_Lk_time += deltatime.seconds + deltatime.microseconds / 1000000

            Lksub1 = Li.copy()
            
            if len(Lksub1) == 0:
                break
            for lk_i in Lksub1:
                self.freq_itemsets.append((lk_i, self.support_data[lk_i]))
            i += 1
        
        print("Create Ck time (s): ", create_Ck_time)
        print("Generate Lk time (s): ", generate_Lk_time)

        print(self.assoc_rules)

        return {'freq_itemsets': self.freq_itemsets,
                'assoc_rules': self.assoc_rules
                }