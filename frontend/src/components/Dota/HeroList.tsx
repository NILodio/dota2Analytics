import { SimpleGrid, Box } from '@chakra-ui/react';
import { Hero } from '../../client/models';
import { HeroThumbnail } from './Thumbnail';



interface HeroListProps {
    heroes: Hero[];
}
  

export const HeroList = ({ heroes }: HeroListProps) => {
    return (
        <SimpleGrid columns={5} spacing="5px">
            {heroes?.map((hero) => {
                return <HeroThumbnail key={hero.id} hero={hero} />;
            })}
        </SimpleGrid>
    );
};
export default HeroList