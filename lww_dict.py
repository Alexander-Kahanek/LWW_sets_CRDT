import time

class LWWhelpers:
    '''
    static helper functions to assist the main LWW class
    '''

    @staticmethod
    def merge_sets(payload1, payload2):
        '''
        helps the LWW.merge() by actually merging the two given Add or Remove payloads

        payload1 : (list) the first payload to merge with
        payload2 : (list) the second payload to merge with
        '''

        

        for ele, time in payload2.items():
            if ele not in payload1.keys():
                # p2 element is not in p1/merged
                payload1[ele] = time
            else:
                # p2 element is in p1/merged
                if time > payload1[ele]:
                    # ele times are different and p2 is greater
                    payload1[ele] = time

        return payload1, payload1

class LWW():
    '''
    Last Writer Wins Element Set with CRDT Implementation

    this allows for using timestamps to add or remove elements from the set.

    lww_id : (any type) the unique id for the LWW element set
    '''

    def __init__(self, lww_id):
        '''
        expects an id to initialize to

        lww_id : (any type) the unique id for the LWW element set
        '''
        self.A = {} # the Add set
        self.R = {} # the Remove set
        self.id = lww_id
        self.helper = LWWhelpers()

    def add(self, element):
        '''
        adds an element to the given LWW

        element : (any type) the element to add
        '''
        if element in self.A.values():
            self.A[element] = 

    def remove(self, element):
        '''
        removes an element to the given LWW

        element : (any type) the element to remove
        '''
        self.R[element] = time.perf_counter()

    def check_element(self, element):
        '''
        checks both add and remove sets for the given element, compares timestamps between the sets for the element

        returns | True if element has most recent timestamp in add set, else returns False
        '''
        if element in self.A.keys():
            # element is in add
            print('add set', self.A.keys())
            print('remove set', self.R.keys())
            if element not in self.R.keys() or self.A[element] > self.R[element]:
                # element is not in remove,
                # or add timestamp is more recent than remove timestamp
                return True
            
            return False

    def compare(self, lww2):
        '''
        compares two LWW objects. checks both Add and Remove set to identify if they are exactly the same.

        lww2 : (LWW object) the second object to compare payloads with
        '''

        return self.A == lww2.A and self.R == lww2.R 

    def merge(self, lww2):
        '''
        merges two LWW objects to both be the same.

        lww2 : (LWW object) the second object to merge LWW objects with
        '''

        if not self.compare(lww2):
            self.A, lww2.A = self.helper.merge_sets(self.A, lww2.A)
            self.R, lww2.R = self.helper.merge_sets(self.R, lww2.R)

    def get_current(self):
        '''
        returns | list of all the elements that are currently in the LWW object
        '''

        return [ele for ele in self.A.keys() if self.check_element(ele)]
            

    def __str__(self):
        return f'LWW obj {self.id} has Add set: {self.A} and Remove set: {self.R}'