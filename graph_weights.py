import networkx as nx
import string

tube_lines = open('tube_lines.txt').read()
lines = tube_lines.split('\n')
lines_idx = []
for idx, value in enumerate(lines):
    if value.startswith('Line:'):
        lines_idx.append([value, idx])

for i in range(len(lines_idx)-1):
    if lines_idx[i][0] == 'Line: Bakerloo':
        bakerloo = lines[(lines_idx[i][1]+1):lines_idx[i+1][1]]

    elif lines_idx[i][0] == 'Line: Jubilee':
        jubilee = lines[(lines_idx[i][1]+1):lines_idx[i+1][1]]

    elif lines_idx[i][0] == 'Line: Victoria':
        victoria = lines[(lines_idx[i][1]+1):lines_idx[i+1][1]]


bak_st = []
for i in range(len(bakerloo)-1):
    bak_st.append((bakerloo[i], bakerloo[i+1]))

jub_st = []
for i in range(len(jubilee)-1):
    jub_st.append((jubilee[i], jubilee[i+1]))

vic_st = []
for i in range(len(victoria)-1):
    vic_st.append((victoria[i], victoria[i+1]))

line_list = [bakerloo, jubilee, victoria]
line_names = ['Line: Bakerloo', 'Line: Jubilee', 'Line: Victoria']
stations = []
for i in line_list:
    for j in i:
        if j not in stations:
            stations.append(j)

G = nx.Graph()
G.add_nodes_from(stations)

def get_distance_one(A, B):
    return 1

def get_distance_letters(A, B):
    letters = string.ascii_lowercase
    for i in range(len(A)):
        if A[i] != B[i]:
            index = []
            for idx, value in enumerate(letters):
                if value == A[i].lower() or value == B[i].lower():
                    index.append(idx)
            return abs(index[0] - index[1]) - 1

def get_distance_latitude(A, B):
    tube_locations = open('tube_locations.txt').read()
    locations = tube_locations.split('\n')
    lists = []
    for i in locations:
        splitted = i.split('\t')
        lists.append(splitted)

    latitudes = []
    for i in lists:
        if i[0] == A or i[0] == B:
            latitudes.append(float(i[1]))
    return abs(float(latitudes[0]) - float(latitudes[1]))


def get_distance(origin, destination, weight_function):

    for i in line_list:
        for j in range(len(i) - 1):
            G.add_edge(i[j], i[j+1], weight=weight_function(i[j], i[j+1]))

    if nx.has_path(G, source=origin, target=destination):
        path = nx.shortest_path(G, source=origin, target=destination)
        print(path)
    else:
        print('There is no path between {0} and {1}'.format(origin, destination))
        return -1


    output = []
    for i in range(len(path) - 2):
        for j in range(len(line_list)):
            if path[i] in line_list[j] and path[i + 1] in line_list[j] and path[i + 2] not in line_list[j]:
                output.append(line_names[j])
                for k in range(len(line_list)):
                    if path[i + 1] in line_list[k] and path[i + 2] in line_list[k]:
                        output.append(line_names[k])

    if len(output) == 0:
        for j in range(len(line_list)):
            if path[0] in line_list[j] and path[-1] in line_list[j]:
                output.append(line_names[j])
    else:
        for i in range(len(output) - 2, -1, -1):
            if output[i] == output[i+1]:
                del output[i+1]
    return output

def part1(origin, destination):
    print(get_distance(origin, destination, get_distance_one))

def part2a(origin, destination):
    print(get_distance(origin, destination, get_distance_letters))


def part2b(origin, destination):
    print(get_distance(origin, destination, get_distance_latitude))



if __name__ == '__main__':

    print("Enter the origin: ")
    origin = input()
    print("Enter the destination: ")
    destination = input()

    part1(origin, destination)
    print('-----------------------------------------------')
    part2a(origin, destination)
    print('-----------------------------------------------')
    part2b(origin, destination)
