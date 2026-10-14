"""PSA abrasive disc, Ø250 (10 in): zirconia or ceramic, 60-120 grit for metal. Bought; peel and replace."""
from steve import Component
from sander_shapes import ycyl
from sander_params import disc_d, disk_face, hub_t, platen_t, abrasive_t

y_back = -disk_face - hub_t - platen_t
abrasive = Component("abrasive", name="PSA abrasive disc Ø250")
abrasive.add("disc", ycyl(disc_d / 2, y_back - abrasive_t, y_back), name="Abrasive disc")
abrasive.material("pc", color="#33456e")             # appearance only (blue zirconia)
