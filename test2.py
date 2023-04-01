import branchpacket

a = branchpacket.BranchResponse(branchpacket.BranchStatus.OK, "b")
print(a.as_json())

try:
    b = branchpacket.BranchResponse("SOND", "b")
except TypeError:
    print("OK")

c = branchpacket.BranchResponse.from_json("{\"statuscode\": 200, \"payload\": \"b\"}")
print(c.as_json())

d = branchpacket.BranchRequest("LOL", "XD")
print(d.as_json())

x = branchpacket.BranchRequest.from_json("{\"command\": \"LOL\", \"payload\": \"XD\"}")
print(x.as_json())
