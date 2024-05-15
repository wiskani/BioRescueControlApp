interface TokenWithNumber extends Token {
    number:string
}
interface TokenWithRescueNumber extends Token {
    rescue_number:string
}

export const GetTransectHerpetofaunaWithSpecies=async(
    props:Token
): Promise < TransectHerpetoWithSpecies[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL}:8080/api/transect_herpetofauna_with_species_and_count`,
                        requestOptions
                        );
        const data = await response.json();
        return data;
}

export const GetTransectTransHerpetofaunaWithSpecies=async(
    props:Token
): Promise <TransectHerpetoTransWithSpeciesData[]> => {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/transect_relocation_with_species_and_count`
            , requestOptions
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

export const GetPointsTransHerpetofaunaWithSpecies=async(
    props:Token
): Promise <PointHerpetoTransloWithSpeciesData[]> => {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/point_relocation_with_species_and_count`
            , requestOptions
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

export const GetRescueHerpetofaunaWithSpecies=async(
    props:Token
): Promise <RescueHerpetoWithSpeciesData[]> => {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/herpetofauna_rescue_with_species`
            , requestOptions
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

export const GetRescueHerpetofaunaWithSpecieByNumber=async(
    props:TokenWithNumber
): Promise <RescueHerpetoWithSpeciesData> => {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/herpetofauna_rescue_with_species/${props.number}`
            , requestOptions
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

export const GetTranslocationHerpetoByRescueNumber=async(
    props:TokenWithRescueNumber
): Promise <TranslocationHerpetoByNumberRescue> => {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/translocation_herpetofauna_with_species/${props.rescue_number}`
            , requestOptions
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
