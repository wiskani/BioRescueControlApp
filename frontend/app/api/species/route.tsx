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

type RescuesSpecieData = FloraRescueSpeciesData | TransectHerpetoWithSpeciesData | RescueMammalsWithSpecieData 

export const RescuesSpecie = async (props:Token): Promise<RescuesSpecieData[]> => { 
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    'http://localhost:8080/api/join/rescues/species',
    requestOptions
  );
  const data = await response.json();
  return data;
}

  
