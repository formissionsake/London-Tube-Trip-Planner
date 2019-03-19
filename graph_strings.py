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

G = nx.Graph()

def part1(A, B):

    G.add_edges_from(bak_st)
    G.add_edges_from(jub_st)
    G.add_edges_from(vic_st)

    if nx.has_path(G, source=A, target=B):
        path = nx.shortest_path(G, source=A, target=B)
        print(len(path))
        print(path)

    else:
        print('There is no way to go from {0} to {1}'.format(A, B))

    line_names = ['Line: Bakerloo', 'Line: Jubilee', 'Line: Victoria']

    output = []
    for i in range(len(path)-2):
        for j in range(len(line_list)):
                if path[i] in line_list[j] and path[i+1] in line_list[j] and path[i+2] not in line_list[j]:
                    output.append(line_names[j])
                    for k in range(len(line_list)):
                        if path[i+1] in line_list[k] and path[i+2] in line_list[k]:
                            output.append(line_names[k])



    if len(output) == 0:
        for j in range(len(line_list)):
            if path[0] in line_list[j] and path[-1] in line_list[j]:
                output.append(line_names[j])
    else:
        for i in range(len(output) - 2, -1, -1):
            if output[i] == output[i+1]:
                del output[i+1]

    print(output)


def part2a(A, B):

    letters = string.ascii_lowercase
    for i in range(len(A)):
        if A[i] != B[i]:
            index = []
            for idx, value in enumerate(letters):
                if value == A[i].lower() or value == B[i].lower():
                    index.append(idx)
            print('distance({0}, {1}) = {2}'.format(A, B, abs(index[0] - index[1]) - 1))
            return abs(index[0] - index[1]) - 1

def part2b(A, B):

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
    print('distance({0}, {1}) = {2}'.format(A, B, abs(float(latitudes[0]) - float(latitudes[1]))))
    return abs(float(latitudes[0]) - float(latitudes[1]))

if __name__ == '__main__':

    print("Enter the origin: ")
    A = input()
    print("Enter the destination: ")
    B = input()

    part1(A, B)
    print('-----------------------------------------------')
    part2a(A, B)
    print('-----------------------------------------------')
    part2b(A, B)

