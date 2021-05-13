import scale_plots
from .scale_ids import mt_ids, elements, specials

class Test():
    '''Object to containing testing
    functions for Scale covariance files
    '''
    def __init__(self, filename):
        print('PARSING {} ...'.format(filename))
        # Parse the covariance file
        self.filename = filename.split('/')[-1]
        self.plots = scale_plots.Plots()
        self.plots.parse_coverx(filename)
        print('{} PARSED SUCCESSFULLY'.format(filename))
        print('-'*50)
        print('BEGINNING TESTING PROCEDURE')
        print('-'*50)

        # Test for reactions not showing up
        mts_pass = self.test_mts()
        print('-'*50)
        # Test for duplicate mt names
        mt_names_pass = self.test_mt_names()
        print('-'*50)
        # Test for materials not showing up
        mats_pass = self.test_mats()
        print('-'*50)
        # Test for dublicate mat names
        mat_names_pass = self.test_mat_names()
        print('-'*50)

        if mts_pass and mt_names_pass and mats_pass and mat_names_pass:
            print('ALL TESTS PASSED')
        else:
            print('TESTS HAVE FAILED scale_ids.py NEEDS UPDATING')
        print('-'*50)

    def test_mts(self):
        print('Testing MT ids...')

        # List of all ids that have a problem
        problem_mts = []
        # Check that all reactions are in the mt_ids dictionary
        for _, mt1, _, mt2 in self.plots.cov_matrices[self.filename].keys():
            # If either reaction is not found in the dictionary print that error
            if mt1 not in mt_ids.keys() and mt1 not in problem_mts:
                print('{} is not found in mt_ids.'.format(mt1))
                problem_mts.append(mt1)
            if mt2 not in mt_ids.keys() and mt2 not in problem_mts:
                print('{} is not found in mt_ids.'.format(mt2))
                problem_mts.append(mt2)

        # Indicate a pass of the test or a fail
        if len(problem_mts) == 0:
            print('MT TEST PASSED')
            return True
        else:
            print('Error found with {} MT id'.format(len(problem_mts)))
            print('MT TEST FAILED ADD MISSING IDS TO scale_plots.py')
            return False

    def test_mt_names(self):
        print('Testing MT names...')

        # Check that all the names are unique
        mt_ids_len = len(mt_ids)
        mt_names = {v: k for k, v in mt_ids.items()}
        mt_names_len = len(mt_names)

        # Passed if the lengths are the same
        if mt_ids_len == mt_names_len:
            print('MT NAMES TEST PASSED')
            return True
        
        # If names are the same find them
        same_names_dict = {}
        for mtid, name in mt_ids.items():
            if name not in same_names_dict.keys():
                same_names_dict[name] = [mtid]
            else:
                same_names_dict[name].append(mtid)

        # Print name and ids for duplicates
        for name, mtids in same_names_dict.items():
            if len(mtids) > 1:
                print('{} is used for: '.format(name), end='')
                print(mtids)
        
        print('MT NAMES TEST FAILED CHANGE ABOVE NAMES')
        return False

    def test_mats(self):
        print('Testing MAT ids...')

        problem_mats = []
        # Check that all special materials have a name
        # and that no material has the same name
        for mat1, _, mat2, _ in self.plots.cov_matrices[self.filename].keys():
            # Check for special cases with 7 digits
            if mat1 // 1000000 > 0:
                # If it is not in the dictionary
                if mat1 not in specials.keys() and mat1 not in problem_mats:
                    print('{} is not found in specials.'.format(mat1))
                    problem_mats.append(mat1)
            
            if mat2 // 1000000 > 0:
                if mat2 not in specials.keys() and mat2 not in problem_mats:
                    print('{} is not found in specials.'.format(mat2))
                    problem_mats.append(mat2)

        # Indicate a pass of the test or a fail
        if len(problem_mats) == 0:
            print('MAT TEST PASSED')
            return True
        else:
            print('MAT TEST FAILED ADD MISSING MATS TO scale_ids.py')
            return False

    def test_mat_names(self):
        print('Testing MAT names...')

        # Create a set of all mat ids
        mats = []
        for mat1, _, mat2, _ in self.plots.cov_matrices[self.filename].keys():
            mats.append(mat1)
            mats.append(mat2)
        mats = set(mats)

        # Create a dictionary for material names
        mat_ids = {}
        for mat in mats:
            mat_ids[mat] = self.plots.get_mat_name(mat)

        # Check that all the names are unique
        mat_ids_len = len(mat_ids)
        mat_names = {v: k for k, v in mat_ids.items()}
        mat_names_len = len(mat_names)

        # Passed if the lengths are the same
        if mat_ids_len == mat_names_len:
            print('MAT NAMES TEST PASSED')
            return True
        # If names are the same find them
        same_names_dict = {}
        for matid, name in mat_ids.items():
            if name not in same_names_dict.keys():
                same_names_dict[name] = [matid]
            else:
                same_names_dict[name].append(matid)

        # Print name and ids for duplicates
        for name, matids in same_names_dict.items():
            if len(matids) > 1:
                print('{} is used for: '.format(name), end='')
                print(matids)
        
        print('MAT NAMES TEST FAILED CHANGE ABOVE NAMES')
        return False
