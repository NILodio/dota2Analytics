import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react";
import { type SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  type ApiError,
  type PollOut,
  type PollUpdate,
  PollsService,
} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";

interface EditPollProps {
  poll: PollOut;
  isOpen: boolean;
  onClose: () => void;
}

const EditPoll = ({ poll, isOpen, onClose }: EditPollProps) => {
  const queryClient = useQueryClient();
  const showToast = useCustomToast();
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, errors, isDirty },
  } = useForm<PollUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: poll,
  });

  const mutation = useMutation({
    mutationFn: (data: PollUpdate) =>
      PollsService.updatePoll({ id: poll.id, requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Poll updated successfully.", "success");
      onClose();
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail;
      showToast("Something went wrong.", `${errDetail}`, "error");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["polls"] });
    },
  });

  const onSubmit: SubmitHandler<PollUpdate> = async (data) => {
    mutation.mutate(data);
  };

  const onCancel = () => {
    reset();
    onClose();
  };

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Edit Poll</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.hero_id}>
              <FormLabel htmlFor="Heri Id">Hero ID</FormLabel>
              <Input
                id="hero_id"
                {...register("hero_id", {
                  required: "Hero Id is required.",
                  pattern: {
                    value: /^[0-9]*$/,
                    message: "Hero Id should be a number.",
                  },
                })}
                placeholder="Hero Id"
                type="number"
              />
              {errors.hero_id && (
                <FormErrorMessage>{errors.hero_id.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.hero_name}>
              <FormLabel htmlFor="hero_name">Hero Name</FormLabel>
              <Input
                id="hero_name"
                {...register("hero_name", {
                  required: "Hero Name is required.",
                })}
                placeholder="Hero Name"
                type="text"
              />
              {errors.hero_name && (
                <FormErrorMessage>{errors.hero_name.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl isRequired isInvalid={!!errors.team}>
              <FormLabel htmlFor="team">Team</FormLabel>
              <Input
                id="team"
                {...register("team", {
                  required: "Team is required.",
                })}
                placeholder="Team"
                type="text"
              />
              {errors.team && (
                <FormErrorMessage>{errors.team.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="player_name">Player Name</FormLabel>
              <Input
                id="player_name"
                {...register("player_name")}
                placeholder="Player Name"
                type="text"
              />
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="description">Description</FormLabel>
              <Input
                id="description"
                {...register("description")}
                placeholder="Description"
                type="text"
              />
            </FormControl>
          </ModalBody>
          <ModalFooter gap={3}>
            <Button
              variant="primary"
              type="submit"
              isLoading={isSubmitting}
              isDisabled={!isDirty}
            >
              Save
            </Button>
            <Button onClick={onCancel}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default EditPoll;
