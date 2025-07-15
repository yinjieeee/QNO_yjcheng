| Property      | Attribute  | Description                                                                                                               |
| ------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| Data          | `Q.data`   | Matrix representing state or operator                                                                                     |
| Dimensions    | `Q.dims`   | List keeping track of shapes for individual components of a multipartite system (for tensor products and partial traces). |
| Shape         | `Q.shape`  | Dimensions of underlying data matrix.                                                                                     |
| is Hermitian? | `Q.isherm` | Is the operator Hermitian or not?                                                                                         |
| Type          | `Q.type`   | Is object of type ‘ket, ‘bra’, ‘oper’, or ‘super’?                                                                        |
