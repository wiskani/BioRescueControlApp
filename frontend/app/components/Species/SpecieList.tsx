import SpecieItem from "./SpecieItem";

interface SpecieListProps {
  species: SpecieItemData[];
}

const SpecieList: React.FC<SpecieListProps> = ({species}) => {
  return (
        <div className="container mx-auto px-4 py-20">
          <h2 className="text-center sm:text-4xl text-2xl font-bold tracking-tight text-gray-800">Especies</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {species.map((specieData, index) => (
                    <SpecieItem key={index} {...specieData} />
                ))}
            </div>
        </div>
    );
}

export default SpecieList;
