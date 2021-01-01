# get a list of all brew packages
import os
import requests
import argparse


def get_formula_information(formulas):
    """Gather information about the given list of formulas.

    Args:
        formulas (list): All formulas that need to be searched.

    Returns:
        dict: Containing result-dicts for found formulas, as well as a list of not found formulas.
    """
    print(f'\n🍺 Collection information about {len(formulas)} packages...')
    results = {
        'formulas': [],
        'not_found': []
    }

    for formula in formulas:
        url = f"https://formulae.brew.sh/api/formula/{formula}.json"
        response = requests.get(url)

        # only store formulas that were successfully queried
        if response.status_code == 200:
            results['formulas'].append(response.json())
        else:
            results['not_found'].append(formula)

    return results


def print_formula_state(formula, architecture, length):
    """Function for deciding what to print per formula

    Args:
        formula (dict): JSON-response for formula, as dict.
        architecture (str): The target architecture, that needs to be queried
        length (int): max length of package name, required for formatting
    """

    package_name = formula['name']
    if 'bottle' in formula and 'stable' in formula['bottle']:

        # check architecture
        bottles = formula['bottle']['stable']['files']

        if architecture in bottles:
            print(
                f"✅ | {package_name:<{length}} | Available for {architecture}!"
                )
        else:
            print(f"🚫 | {package_name:<{length}} | Not available right now")

    else:
        print(f"❌ | {package_name:<{length}} | No stable version")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Checks your currently installed brew formulas for compatibility with certain architectures.')
    parser.add_argument('--architecture', type=str, default='arm64_big_sur',
                        help='Architecture to look for (default: arm64_big_sur)', required=False)

    args = parser.parse_args()

    # get formula list
    brew_list = os.popen('brew list --formula -1').read().strip().split('\n')

    # retrieve information for each formula
    res = get_formula_information(brew_list)

    # print information for found formulas
    forms = res['formulas']
    length = len(max(brew_list, key=len))

    # print available forms
    titles = ['Package Name', 'State']
    print(f'\n🍺 | {titles[0]:<{length}} | {titles[1]}')
    max_len = 25 + length + len(args.architecture)
    print("-" * max_len)
    
    # print all found formulas
    for f in forms:
        print_formula_state(f, args.architecture, length)

    # print forms that were not found
    print(f"\n🍺 The following formulae were not found...")
    print("-" * max_len)
    for f in res['not_found']:
        print(f'❓ - {f:<{length}} - Formula not found, check manually please.')
