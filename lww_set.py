import time

class LWWhelpers:
    '''
    static helper functions to assist the main LWW class
    '''

    @staticmethod
    def update_set(payload, element):
        '''
        helps the LWW.add() and LWW.remove() to add an element to the chose Add or Remove set

        set : (list) the Add or Remove set from the LWW object
        element : (any type) the element to be added to the set

        returns | the updated set
        '''
        
        # if payload is not None:
        for i, item in enumerate(payload):
            if item['element'] == element: # element is already included in the set, so just update time
                payload[i]['timestamp'] = time.perf_counter()
                return payload

        # element was not included in the set, so add it
        payload.append({'element': element, 'timestamp': time.perf_counter()})
        payload.sort(key = lambda x: x['timestamp'])
        return payload

    @staticmethod
    def merge_sets(payload1, payload2):
        '''
        helps the LWW.merge() by actually merging the two given Add or Remove payloads

        payload1 : (list) the first payload to merge with
        payload2 : (list) the second payload to merge with
        '''

        merged = payload1
        p1_elements = [item['element'] for item in payload1]

        for item2 in payload2:
            if item2['element'] not in p1_elements:
                # p2 item is not in p1/merged
                merged.append(item2)
            else:
                # p2 item is in p1/merged
                for i in range(len(merged)):
                    # find the existing matched item in merged and update if timestamp is less recent in merged
                    if merged[i]['element'] == item2['element'] and merged[i]['timestamp'] < item2['timestamp']:
                        merged[i]['timestamp'] = item2['timestamp']

        return merged, merged

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
        self.A = [] # the Add set
        self.R = [] # the Remove set
        self.id = lww_id
        self.helper = LWWhelpers()

    def add(self, element):
        '''
        adds an element to the given LWW

        element : (any type) the element to add
        '''

        self.A = self.helper.update_set(self.A, element)

    def remove(self, element):
        '''
        removes an element to the given LWW

        element : (any type) the element to remove
        '''

        self.R = self.helper.update_set(self.R, element)

    def check_element(self, element):
        '''
        checks both add and remove sets for the given element, compares timestamps between the sets for the element

        returns | True if element has most recent timestamp in add set, else returns False
        '''
        times_in_add = [item['timestamp'] for item in self.A if item['element'] == element]

        if len(times_in_add) != 0:
            times_in_rem = [item['timestamp'] for item in self.R if item['element'] == element]

            if len(times_in_rem) == 0 or times_in_add[-1] > times_in_rem[-1]:
                # element does not exist in remove set, but does in add set
                # or the elements add time is more recent than the remove time
                # these are the only conditions for keeping an element in the add set
                return True
        return False

    def compare(self, lww2):
        '''
        compares two LWW objects. checks both Add and Remove set to identify if they are exactly the same.

        lww2 : (LWW object) the second object to compare payloads with

        returns | true if Add set and Remove set are exactly the same
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
        return [item for item in self.A if self.check_element(item['element'])]

    def __str__(self):
        return f'LWW obj {self.id} has Add set: {self.A} and Remove set: {self.R}'