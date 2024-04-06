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
  } from "@chakra-ui/react"
  import { type SubmitHandler, useForm } from "react-hook-form"
  import { useMutation, useQueryClient } from "@tanstack/react-query"
  
  import { type ApiError, type ItemCreate, ItemsService, HeroOut, HeroPollCreate} from "../../client"
  import useCustomToast from "../../hooks/useCustomToast"
  
  interface AddHeroPolProps {
    hero: HeroOut
    isOpen: boolean
    onClose: () => void
  }
  
  const AddHeroPoll = ({ isOpen, onClose }: AddHeroPolProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
      register,
      handleSubmit,
      reset,
      formState: { errors, isSubmitting },
    } = useForm<HeroPollCreate>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: {
        hero_id: 0,
        hero_name: "",
        team: "",
        description: "",
      },
    })
    const mutation = useMutation({
      mutationFn: (data: HeroPollCreate) =>
        ItemsService.createItem({ requestBody: data }),
      onSuccess: () => {
        showToast("Success!", "Hero Poll created successfully.", "success")
        reset()
        onClose()
      },
      onError: (err: ApiError) => {
        const errDetail = (err.body as any)?.detail
        showToast("Something went wrong.", `${errDetail}`, "error")
      },
      onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ["items"] })
      },
    })
  
    const onSubmit: SubmitHandler<ItemCreate> = (data) => {
      mutation.mutate(data)
    }
  
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
            <ModalHeader>Add Item</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl isRequired isInvalid={!!errors.title}>
                <FormLabel htmlFor="title">Title</FormLabel>
                <Input
                  id="title"
                  {...register("title", {
                    required: "Title is required.",
                  })}
                  placeholder="Title"
                  type="text"
                />
                {errors.title && (
                  <FormErrorMessage>{errors.title.message}</FormErrorMessage>
                )}
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
              <Button variant="primary" type="submit" isLoading={isSubmitting}>
                Save
              </Button>
              <Button onClick={onClose}>Cancel</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    )
  }
  
  export default AddHeroPoll
  