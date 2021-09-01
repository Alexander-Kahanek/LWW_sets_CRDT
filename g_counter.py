class GCounter():
    '''
    a grow only counter with CRDT implementation

    this unique G Counter, g_id, stores all independent nodes as a dictionary, eles, to track
    each running GCounter and give an estimated value without the need for talking

    each GCounter relates to one client side user. multple counters
    are used in tandem to asynchronously update counter values.

    g_id : (any type) the unique identifier for the counter
    '''
    def __init__(self, g_id):
        '''
        expects initialization to be just an id for the g_counter node

        g_id : (any type) the unique identifier for the counter
        '''
        self.eles = {} # dictionary for storing the elements
        self.id = g_id

    def add_node(self, ele_id):
        '''
        expects the id for the G_counter element node

        only initializes an element value to 0

        ele_id : (any type) the unique identifier for the node
        '''

        self.eles[ele_id] = 0

    def increment(self, ele_id):
        '''
        increments a node using its ele_id

        if the element has not been defined, it will define and increment the element

        ele_id : (any type) the unique identifier for the node to increment
        '''

        try:
            self.eles[ele_id] += 1
        except Exception as e:
            print(f'{e}')

    def get_value(self):
        '''
        returns | all the last known values for the counter
        '''

        return sum(self.eles.values())

    def merge(self, GC2):
        '''
        updates max values for all elements in the both g counters

        if there are elements not seen by either counter, that exists in the other counter, it then updates both counters first to initilize the unseen elements

        GC2 : (GCounter object) the GCounter to merge with
        '''

        if self.eles.keys() != GC2.eles.keys():
            # elements are not the same
            # add elements not in both to each GCounter
            self.eles.update({ele_id:0 for ele_id in GC2.eles.keys() if ele_id not in self.eles.keys()})
            GC2.eles.update({ele_id:0 for ele_id in self.eles.keys() if ele_id not in GC2.eles.keys()})
        
        max_values = {ele_id: max(val, GC2.eles[ele_id])
                      for ele_id, val in self.eles.items()}

        # update both counters
        self.eles = max_values
        GC2.eles = max_values

    def print_gc(self):
        '''
        prints the counters current state
        '''

        print(f'g counter node {self.id} = {self.eles}, sum = {self.get_value()}')