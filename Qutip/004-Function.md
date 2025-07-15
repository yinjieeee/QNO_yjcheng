| Function         | Command                     | Description                                                             |
| ---------------- | --------------------------- | ----------------------------------------------------------------------- |
| Check Hermicity  | `Q.check_herm()`            | Check if quantum object is Hermitian                                    |
| Conjugate        | `Q.conj()`                  | Conjugate of quantum object.                                            |
| Cosine           | `Q.cosm()`                  | Cosine of quantum object.                                               |
| Dagger (adjoint) | `Q.dag()`                   | Returns adjoint (dagger) of object.                                     |
| Diagonal         | `Q.diag()`                  | Returns the diagonal elements.                                          |
| Diamond Norm     | `Q.dnorm()`                 | Returns the diamond norm.                                               |
| Eigenenergies    | `Q.eigenenergies()`         | Eigenenergies (values) of operator.                                     |
| Eigenstates      | `Q.eigenstates()`           | Returns eigenvalues and eigenvectors.                                   |
| Eliminate States | `Q.eliminate_states(inds)`  | Returns quantum object with states in list inds removed.                |
| Exponential      | `Q.expm()`                  | Matrix exponential of operator.                                         |
| Extract States   | `Q.extract_states(inds)`    | Qobj with states listed in inds only.                                   |
| Full             | `Q.full()`                  | Returns full (not sparse) array of Q’s data.                            |
| Groundstate      | `Q.groundstate()`           | Eigenval & eigket of Qobj groundstate.                                  |
| Matrix Element   | `Q.matrix_element(bra,ket)` | Matrix element <bra\|Q\|ket>                                            |
| Norm             | `Q.norm()`                  | Returns L2 norm for states, trace norm for operators.                   |
| Overlap          | `Q.overlap(state)`          | Overlap between current Qobj and a given state.                         |
| Partial Trace    | `Q.ptrace(sel)`             | Partial trace returning components selected using ‘sel’ parameter.      |
| Permute          | `Q.permute(order)`          | Permutes the tensor structure of a composite object in the given order. |
| Projector        | `Q.proj()`                  | Form projector operator from given ket or bra vector.                   |
| Sine             | `Q.sinm()`                  | Sine of quantum operator.                                               |
| Sqrt             | `Q.sqrtm()`                 | Matrix sqrt of operator.                                                |
| Tidyup           | `Q.tidyup()`                | Removes small elements from Qobj.                                       |
| Trace            | `Q.tr()`                    | Returns trace of quantum object.                                        |
| Transform        | `Q.transform(inpt)`         | A basis transformation defined by matrix or list of kets ‘inpt’ .       |
| Transpose        | `Q.trans()`                 | Transpose of quantum object.                                            |
| Truncate Neg     | `Q.trunc_neg()`             | Truncates negative eigenvalues                                          |
| Unit             | `Q.unit()`                  | Returns normalized (unit) vector Q/Q.norm().                            |