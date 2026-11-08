"""Front idler. A plain drum the shoe wraps. It does not drive."""
from steve import Component
from params import idler_r

idler = Component("idler", name="Front idler")

idler.cylinder("drum", idler_r, 160, at=(0, -80, 0), direction=(0, 1, 0))
idler.cylinder("pocket_a", idler_r - 40, 55, at=(0, -75, 0), direction=(0, 1, 0), op="cut")
idler.cylinder("pocket_b", idler_r - 40, 55, at=(0, 20, 0), direction=(0, 1, 0), op="cut")
idler.cylinder("bore", 80, 180, at=(0, -90, 0), direction=(0, 1, 0), op="cut")

idler.material("steel-34crnimo6", finish="machined", color="#4a4f57")
