export async function getReservas(usuario) {
  let respuesta = await fetch(
    "http://lb-parcial-347173395.us-east-1.elb.amazonaws.com:5003/reservas/" +
      usuario,
    {
      method: "GET",
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
