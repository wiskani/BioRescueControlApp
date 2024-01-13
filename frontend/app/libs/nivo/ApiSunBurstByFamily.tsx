export const GetSunburstByFamily= async (props: Token): Promise<SunBurstFamilyData> => {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}:8080/api/nivo/sunburst`,
    requestOptions
  );
  const data = await response.json();
  return data;
}
