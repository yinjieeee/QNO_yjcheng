| Operators                           | Command (# means optional) | Inputs                                                                        |
| ----------------------------------- | -------------------------- | ----------------------------------------------------------------------------- |
| Charge operator                     | `charge(N,M=-N)`           | Diagonal operator with entries from M..0..N.                                  |
| Commutator                          | `commutator(A, B, kind)`   | Kind = ‘normal’ or ‘anti’.                                                    |
| Diagonals operator                  | `qdiags(N)`                | Quantum object created from arrays of diagonals at given offsets.             |
| Displacement operator (Single-mode) | `displace(N,alpha)`        | N=number of levels in Hilbert space, alpha = complex displacement amplitude.  |
| Higher spin operators               | `jmat(j,#s)`               | j = integer or half-integer representing spin, s = ‘x’, ‘y’, ‘z’, ‘+’, or ‘-‘ |
| Identity                            | `qeye(N)`                  | N = number of levels in Hilbert space.                                        |
| Lowering (destruction) operator     | `destroy(N)`               | same as above                                                                 |
| Momentum operator                   | `momentum(N)`              | same as above                                                                 |
| Number operator                     | `num(N)`                   | same as above                                                                 |
| Phase operator (Single-mode)        | `phase(N, phi0)`           | Single-mode Pegg-Barnett phase operator with ref phase phi0.                  |
| Position operator                   | `position(N)`              | same as above                                                                 |
| Raising (creation) operator         | `create(N)`                | same as above                                                                 |
| Squeezing operator (Single-mode)    | `squeeze(N, sp)`           | N=number of levels in Hilbert space, sp = squeezing parameter.                |
| Squeezing operator (Generalized)    | `squeezing(q1, q2, sp)`    | q1,q2 = Quantum operators (Qobj) sp = squeezing parameter.                    |
| Sigma-X                             | `sigmax()`                 |                                                                               |
| Sigma-Y                             | `sigmay()`                 |                                                                               |
| Sigma-Z                             | `sigmaz()`                 |                                                                               |
| Sigma plus                          | `sigmap()`                 |                                                                               |
| Sigma minus                         | `sigmam()`                 |                                                                               |
| Tunneling operator                  | `tunneling(N,m)`           | Tunneling operator with elements of the form \|N><N+m\|+\|N+m><N\|.           |