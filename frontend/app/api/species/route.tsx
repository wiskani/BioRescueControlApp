interface TokenWithSpecieName extends Token {
        specie_id: number;
}

type RescuesSpecieData =
        | FloraRescueSpeciesData
        | TransectHerpetoWithSpeciesData
        | RescueMammalsWithSpecieData 

export const SpeciesItem = async (props:Token): Promise<SpecieItemData[]> => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    'http://localhost:8080/api/join/species',
    requestOptions
  );
  const data = await response.json();
  return data;
}


export const RescuesSpecie = async (props:TokenWithSpecieName): Promise<RescuesSpecieData[]> => { 
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    `http://localhost:8080/api/specie/rescues/${props.specie_id}`,
    requestOptions
  );
  const data = await response.json();
  return data;
}

  
