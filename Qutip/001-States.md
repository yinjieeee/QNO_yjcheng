| States                                       | Command (# means optional) | Inputs                                                                                   |
| -------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------- |
| Fock state ket vector                        | `basis(N,#m)`/`fock(N,#m)` | N = number of levels in Hilbert space, m = level containing excitation (0 if no m given) |
| Fock density matrix (outer product of basis) | `fock_dm(N,#p)`            | same as basis(N,m) / fock(N,m)                                                           |
| Coherent state                               | `coherent(N,alpha)`        | alpha = complex number (eigenvalue) for requested coherent state                         |
| Coherent density matrix (outer product)      | `coherent_dm(N,alpha)`     | same as coherent(N,alpha)                                                                |
| Thermal density matrix (for n particles)     | `thermal_dm(N,n)`          | n = particle number expectation value                                                    |
