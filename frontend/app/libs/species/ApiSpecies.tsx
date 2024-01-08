interface TokenWithSpecieName extends Token {
        specie_id: number;
}

type RescuesSpecieData =
        | FloraRescueSpeciesData
        | TransectHerpetoWithSpeciesData
        | RescueMammalsWithSpecieData 

export const GetSpeciesItem = async (props:Token): Promise<SpecieItemData[]> => {
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

export const GetRescuesSpecie = async (props: TokenWithSpecieName): Promise<RescuesSpecieData[]> => {
  try {
    const requestOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + props.token,
      },
    };
    const response = await fetch(
      `http://localhost:8080/api/specie/rescues/${props.specie_id}`,
      requestOptions
    );

    if (!response.ok) {
      const errorDetails = await response.json();
      throw new Error(errorDetails.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data: ', error);
    throw error;  // Re-throw the error to be handled by the caller
  }
}

