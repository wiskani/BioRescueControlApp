export const GetBarChartFloraByFamily= async (
    props: Token
): Promise<BarChartFamilyData[]> => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/nivo/barchart/flora`,
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
