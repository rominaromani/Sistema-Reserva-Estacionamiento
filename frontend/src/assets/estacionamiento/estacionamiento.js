export async function obtenerEstacionamientos() {
  let respuesta = await fetch(
    "http://lb-parcial-347173395.us-east-1.elb.amazonaws.com:5004/estacionamiento",
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

export function calcularCosto(fechaInicio, fechaFin) {
  if (fechaInicio != null && fechaFin != null) {
    let valorFechaFin = Date.parse(fechaFin);
    let valorFechaInicio = Date.parse(fechaInicio);

    let horasTotales = (valorFechaFin - valorFechaInicio) / 1000 / 60 / 60;
    horasTotales =
      Math.floor(horasTotales) +
      1 * (horasTotales - Math.floor(horasTotales) > 0);
    const costo = horasTotales * 3;
    return costo;
  } else {
    return 0;
  }
}
