import { Flex, Text } from "@chakra-ui/react";

interface HeroToolbarProps {
    children: React.ReactNode;
}

export const HeroNavbar= ({ children }: HeroToolbarProps) => {
    return (
        <Flex
            direction={{ base: "column", sm: "row" }}
            gap={{ base: "sm", sm: "lg" }}
            justify={{ sm: "space-between" }}
            align={{ sm: "center" }}
            paddingY="4"
            paddingX={{ base: "4", sm: "8" }}
        >
            <Text fontSize="md" fontWeight="bold" color="gray.700">
                Filter Hero
            </Text>
            {children}
        </Flex>
    );
};
export default HeroNavbar