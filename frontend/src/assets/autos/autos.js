export async function obtenerAutoUsuario(usuario, token) {
  let respuesta = await fetch(
    "http://lb-parcial-347173395.us-east-1.elb.amazonaws.com:5002/autos/" +
      usuario,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
    }
  )
    .then(function (response) {
      return response.json();
    })
    .then(function (responseJson) {
      return responseJson;
    })
    .catch((error) => console.log(error));
  return respuesta;
}
