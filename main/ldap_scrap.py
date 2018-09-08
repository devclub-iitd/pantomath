import ldap

def initialize_ldap ():
    """
    Initialize the connection to IITD LDAP server
    """
    l = ldap.initialize('ldap://ldap1.iitd.ac.in')

    # Bind to server
    try:
        binddn = "dc=iitd,dc=ernet,dc=in"
        l.protocol_version = ldap.VERSION3
        l.simple_bind(binddn)
    except ldap.LDAPError as e:
        if type(e.message) == dict and e.message.has_key('desc'):
            print (e.message['desc'])
        else: 
            print (e)

        raise ConnectionError("Problem with LDAP Binding")
    return l


def perform_search(OU, department, searchFilter, searchAttribute=[]):
    # Set Up LDAP
    l = initialize_ldap()

    # Set up Search
    searchScope = ldap.SCOPE_SUBTREE
    basedn = "ou={},dc={},dc=iitd,dc=ernet,dc=in".format(OU, department)
    res = l.search_s(basedn, searchScope, searchFilter, searchAttribute)

    # Unbind LDAP
    unbind_ldap (l)

    # return the results
    return res


def unbind_ldap(l):
    l.unbind_s()


def get_code_to_dept():
    return {
        "ce":"civil",
        "ch":"chemical",
        "cs":"cse",
        "bb":"dbeb",
        "ee":"ee",
        "mt":"maths",
        "me":"mech",
        "ph":"physics",
        "tt":"textile"
    }


def get_departmental_records(category):
    """
    Category is the 5 digit deparment code (like cs, ee, ...) followed by group and year
    Ex. cs116

    Returns an array of the following structure
    [
        {
            "Name": "...",
            "Entry": "...",
            "UID": "..."
        }, ...
    ]
    """

    code2dept = get_code_to_dept()
    
    # Error checking
    if (len(category) != 5 or (not (category[:2] in code2dept))):
        return []

    # get the department
    department = code2dept[category[:2]]
    
    # Make the search query
    searchFilter = "(uid={}*)".format(category)
    searchAttribute = ["uid", "username", "uniqueIITDid"]   
    search_results = perform_search('IITDpersonDetails', department, searchFilter, searchAttribute) 

    # Put the results in the array
    results = []
    for student in search_results:
        student_info = student[1]
        results.append({
            "Name": student_info['username'][0],
            "Entry": student_info['uniqueIITDid'][0],
            "UID":  student_info['uid'][0]
        })

    # Return the results
    return results


def get_student_info(uid, searchAttributes=["department", "category", "username", "altEmail"]):
    """
    Get the student info
    searchAttributes include:
    department, category, username, altEmail, uniqueIITDid, dateOfBirth, gender, bloodGroup, suspended, emailalias
    Returns an object, indexed by the searchAttributes
    """

    # Error Checking
    if (len(uid) != 9):
        return {}

    # get the department
    category = uid[:2]
    code2dept = get_code_to_dept()
    department = code2dept[category[:2]]

    # Make the search query
    searchFilter = "(uid={})".format(uid)
    searchAttribute = searchAttributes 
    search_results = perform_search('IITDpersonDetails', department, searchFilter, searchAttribute) 

    # Extract and return the results
    if (len(search_results) < 1):
        # The UID does not exist
        return {}
    else:
        result = {}
        for attib, val in (search_results[0][1]).items():
            result[attib] = val[0]
        return result


    
if __name__ == '__main__':
    # l = initialize_ldap()

    searchFilter = "uid=cs1150210"
    searchFilter = "uid=cs1150210"
    searchFilter = "(&(category=mtech)(department=cse))"
    searchFilter = "(&(department=cse)(uid=cs116*))"
    # searchFilter = "(department=cse)"
    searchFilter = "(uid=cs1160321)"
    # searchFilter = None
    searchAttribute = ["gender", "kdl", "username"]   
    searchAttribute=None
    # searchAttribute = ["uid", "username", "uniqueIITDid"]   

    # res = perform_search('IITDpersonDetails', 'cse', searchFilter, searchAttribute)  
    # print (res)

    res = get_student_info('cs1160321')
    res = get_departmental_records('csz15')
    print (res)
    # unbind_ldap(l)

