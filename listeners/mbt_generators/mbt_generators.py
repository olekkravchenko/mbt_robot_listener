import random


class MBTGenerator(object):

    def __init__(self, model):
        self.model = model

    def select_transition_from_current_state(self):
        raise NotImplementedError("Transition selection is not implemented")


class MBTRandomGenerator(MBTGenerator):

    def select_transition_from_current_state(self, current_state):
        transition = random.choice(self.model[current_state])
        return transition


class MBTRandomWeightedGenerator(MBTGenerator):

    def get_random_transition_index(self, transitions):
        weights = [transition[-1] for transition in transitions]
        accumulated_weights = [weights[0]]
        for i in xrange(1, len(weights)):
            accumulated_weights.append(weights[i] + accumulated_weights[i-1])
        selector = random.randrange(0, accumulated_weights[-1])
        index = (index for index, weight in enumerate(accumulated_weights) if weight > selector).next()
        return index

    def select_transition_from_current_state(self, current_state):
        index = self.get_random_transition_index(self.model[current_state])
        transition = self.model[current_state][index]
        return transition


class MBTGeneratorFactory(object):

    @staticmethod
    def create_generator(algorithm_name, model):
        if algorithm_name.lower() == 'random':
            return MBTRandomGenerator(model=model)
        elif algorithm_name.lower() == 'random_weighted':
            return MBTRandomWeightedGenerator(model=model)
        else:
            raise NotImplementedError("Unknown MBT generator algorithm {}".format(algorithm_name))
