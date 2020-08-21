def select_all():
  d = {}
  l = []
  values = [(1, 'Sherzod'), (2, 'Begzod')]
  columns = ('id', 'name')

  for i in values:
    for j in range(2):
      d.update({columns[j]: i[j]})
    l.append(d)
    # d={}
    print(id(d))
    # l.append(dict(d))

  return l
print(select_all())