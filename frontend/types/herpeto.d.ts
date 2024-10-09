export {}

declare global {
    interface TransectHerpetoTransWithSpeciesData{
        cod: string; 
        date: Date;
        latitude_in: number;
        longitude_in: number;
        altitude_in: number;
        latitude_out: number;
        longitude_out: number;
        altitude_out: number;
        specie_names: string[];
        total_translocation: number;
    }

    interface PointHerpetoTransloWithSpeciesData{
        cod: string;
        date: Date;
        latitude: number; 
        longitude: number; 
        altitude: number; 
        specie_names: string[];
        total_translocation: number; 
    }

    interface TransectHerpetoWithSpeciesData {
        number: string; 
        date_in: Date; 
        date_out: Date; 
        latitude_in: number; 
        longitude_in: number; 
        latitude_out: number; 
        longitude_out: number; 
        specie_names: string[]; 
        total_rescue: number; 
    }

    interface RescueHerpetoWithSpeciesData {
        number: string;
        date_rescue: Date; 
        gender: string | null;
        specie_name: string;
        age_group_name: string | null;
        altitude_in: number; 
        latitude_in: number;
        longitude_in: number; 
        altitude_out: number; 
        latitude_out: number; 
        longitude_out: number; 
    }

    interface TransectTranslocationHerpetoWithMarkData {
        cod: string;
        date: Date;
        latitude_in: number;
        longitude_in: number;
        latitude_out: number;
        longitude_out: number;
        number_mark: number;
        code_mark: string | null;
        LHC: number | null;
        weight: number | null;
        is_photo_mark: boolean;
        is_elastomer_mark: boolean;
    }

    interface PointTranslocationHerpetoWithMarkData {
        cod: string;
        date: Date;
        latitude: number;
        longitude: number;
        altitude: number;
        number_mark: number;
        code_mark: string | null;
        LHC: number| null;
        weight: number| null;
        is_photo_mark: booleal;
        is_elastomer_mark: boolean;
    }

    interface TransectHerpetofaunaTranslocationData {
        cod: string;
        date: Date;
        latitude_in: number;
        longitude_in: number;
        altitude_in: number;
        latitude_out: number;
        longitude_out: number;
        altitude_out: number;
    }
    type TranslocationHerpetoByNumberRescue = 
    |TransectTranslocationHerpetoWithMarkData 
    |PointTranslocationHerpetoWithMarkData
    |TransectHerpetofaunaTranslocationData[]

}
