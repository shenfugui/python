def dfs(u, path, st, n):
    if u == n:
        for i in range(n):
            print(path[i])

    for i in range(n):
        if not st[i]:
            path[u] = i
            st[i] = True
            dfs(u + 1, path, st, n)
            st[i] = False


def main():
    path = []
    st = []
    for x in range(30):
        path.append(0)
        st.append(False)
    n = input()
    dfs(0, path, st, int(n))


if __name__ == '__main__':
    main()
